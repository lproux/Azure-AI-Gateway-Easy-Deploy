# Cell 135 Fix - Option A: Auto-Add Current IP to Cosmos Firewall

# Cosmos DB message storage with auto-firewall configuration

from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError
import subprocess
import time

# Resolve endpoint/key (prefer existing vars, then env, then deployment outputs; guard missing step3_outputs)
_step3 = globals().get('step3_outputs', {}) or {}
cosmos_endpoint = globals().get('cosmos_endpoint') or os.getenv('COSMOS_ENDPOINT') or _step3.get('cosmosDbEndpoint')
cosmos_key = globals().get('cosmos_key') or os.getenv('COSMOS_KEY') or _step3.get('cosmosDbKey')

if not cosmos_endpoint or not cosmos_key:
    print('[WARN] Cosmos DB configuration missing (endpoint/key) - persistence disabled')
    cosmos_enabled = False
else:
    cosmos_enabled = True

# OPTION A: Auto-configure Cosmos DB firewall
def auto_configure_cosmos_firewall():
    """Automatically add current IP to Cosmos DB firewall"""
    try:
        # Get current IP
        print('[auto-fix] Detecting current IP address...')
        result = subprocess.run(['curl', '-s', 'ifconfig.me'], capture_output=True, text=True, timeout=5)
        current_ip = result.stdout.strip()
        print(f'[auto-fix] Current IP: {current_ip}')

        # Get Cosmos account name
        cosmos_account = os.environ.get('COSMOS_ACCOUNT_NAME') or 'cosmos-pavavy6pu5hpa'
        resource_group = os.environ.get('RESOURCE_GROUP') or 'lab-master-lab'

        # Add IP to firewall
        print(f'[auto-fix] Adding IP {current_ip} to Cosmos DB firewall...')
        result = subprocess.run([
            'az', 'cosmosdb', 'update',
            '--resource-group', resource_group,
            '--name', cosmos_account,
            '--ip-range-filter', current_ip
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print('[auto-fix] ✅ Firewall updated successfully. Waiting 10s for propagation...')
            time.sleep(10)
            return True
        else:
            print(f'[auto-fix] ❌ Failed: {result.stderr[:200]}')
            return False
    except Exception as e:
        print(f'[auto-fix] ❌ Auto-configuration failed: {e}')
        return False

# Initialize client once (only if enabled)
if cosmos_enabled and 'cosmos_client' not in globals():
    try:
        cred_obj = credential if 'credential' in globals() else cosmos_key
        cosmos_client = CosmosClient(cosmos_endpoint, credential=cred_obj)
    except Exception as e:
        print(f'[ERROR] CosmosClient init failed: {e}')
        cosmos_enabled = False

db_name = 'chatStore'
container_name = 'messages'
container = None

# Create database / container if network/firewall permits
if cosmos_enabled:
    try:
        database = cosmos_client.create_database_if_not_exists(id=db_name)
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path='/threadId'),
            offer_throughput=400
        )
    except CosmosHttpResponseError as e:
        if getattr(e, 'status_code', None) == 403:
            print('[WARN] Cosmos DB access forbidden (likely firewall). Attempting auto-fix...')

            # Try auto-fix
            if auto_configure_cosmos_firewall():
                # Retry connection
                print('[auto-fix] Retrying Cosmos DB connection...')
                try:
                    database = cosmos_client.create_database_if_not_exists(id=db_name)
                    container = database.create_container_if_not_exists(
                        id=container_name,
                        partition_key=PartitionKey(path='/threadId'),
                        offer_throughput=400
                    )
                    print('[auto-fix] ✅ Successfully connected to Cosmos DB after firewall update')
                except Exception as retry_ex:
                    print(f'[auto-fix] ❌ Connection still failed after firewall update: {retry_ex}')
                    cosmos_enabled = False
            else:
                print('')
                print('📋 MANUAL FIX REQUIRED:')
                print('   Azure Portal → Cosmos DB → Networking → Add my current IP → Save')
                print('')
                cosmos_enabled = False
        else:
            print(f'[ERROR] Init Cosmos unexpected HTTP error: {e}')
            cosmos_enabled = False
    except Exception as e:
        print(f'[ERROR] Init Cosmos: {e}')
        cosmos_enabled = False

def store_chat_messages(thread_id: str, msgs: list):
    """
    Persist chat messages (list of {'role','content'}) to Cosmos DB (if enabled),
    otherwise no-op without raising errors.
    """
    if not cosmos_enabled or container is None:
        print('[INFO] Cosmos disabled; skipping message persistence')
        return
    stored = 0
    for idx, m in enumerate(msgs):
        try:
            doc = {
                'id': f'{thread_id}-{idx}',
                'threadId': thread_id,
                'index': idx,
                'role': m.get('role'),
                'content': m.get('content'),
            }
            container.upsert_item(doc)
            stored += 1
        except CosmosHttpResponseError as ex:
            if getattr(ex, 'status_code', None) == 403:
                print('[WARN] Firewall blocked mid-write; disabling persistence')
                break
            else:
                print(f'[WARN] HTTP store failure {idx}: {ex}')
        except Exception as ex:
            print(f'[WARN] Failed to store message {idx}: {ex}')
    print(f'[OK] Stored {stored}/{len(msgs)} messages in Cosmos DB' if cosmos_enabled else '[INFO] No messages stored')

# Example: store existing conversation if available
if 'conversation' in globals():
    store_chat_messages('conv-001', conversation)
else:
    print('[INFO] No conversation variable found to persist')

print(f'Cosmos DB endpoint: {cosmos_endpoint}')
print(f'[OK] Message storage {"enabled" if cosmos_enabled else "disabled"}')
