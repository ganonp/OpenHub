from pyhap.encoder import AccessoryEncoder
import json


class HubEncoder(AccessoryEncoder):

    @staticmethod
    def persist(fp, state):
        """Persist the state of the given Accessory to the given file object.

        Persists:
            - MAC address.
            - Public and private key.
            - UUID and public key of paired clients.
            - Config version.
        """
        paired_clients = {
            str(client): bytes.hex(key) for client, key in state.paired_clients.items()
        }
        config_state = {
            "mac": state.mac,
            "config_version": state.config_version,
            "paired_clients": paired_clients,
            "private_key": bytes.hex(state.private_key.to_seed()),
            "public_key": bytes.hex(state.public_key.to_bytes()),
        }
        json.dump(config_state, fp)

    @staticmethod
    def load_into(fp, state):
        """Load the accessory state from the given file object into the given Accessory.

        @see: AccessoryEncoder.persist
        """
        loaded = json.load(fp)
        state.mac = loaded["mac"]
        state.config_version = loaded["config_version"]
        state.paired_clients = {
            uuid.UUID(client): bytes.fromhex(key)
            for client, key in loaded["paired_clients"].items()
        }
        state.private_key = ed25519.SigningKey(bytes.fromhex(loaded["private_key"]))
        state.public_key = ed25519.VerifyingKey(bytes.fromhex(loaded["public_key"]))
