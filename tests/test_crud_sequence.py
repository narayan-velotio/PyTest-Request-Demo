import pytest
from tests.base_test import BaseTest

class TestCRUDSequence(BaseTest):
    """Test CRUD operations in sequence: GET -> POST -> PUT -> PATCH -> DELETE"""

    def test_crud_sequence(self, product_schema):
        """Test complete CRUD sequence for a MacBook object"""
        # Step 1: GET initial state
        print("\n1. Testing GET - Initial State")
        response = self.api_client.get(self.get_full_url("objects"))
        self.assert_status_code(response, 200)
        initial_objects = response.json()
        print(f"Initial object count: {len(initial_objects)}")

        # Step 2: POST - Create new MacBook
        print("\n2. Testing POST - Create MacBook")
        create_payload = {
            "name": "Apple MacBook Pro 16",
            "data": {
                "year": 2023,
                "price": 1999.99,
                "CPU model": "M2 Max",
                "Hard disk size": "1 TB"
            }
        }
        post_response = self.api_client.post(
            self.get_full_url("objects"),
            json=create_payload
        )
        self.assert_status_code(post_response, 200)
        created_object = post_response.json()
        object_id = created_object['id']
        print(f"Created object ID: {object_id}")
        self.validate_response_schema(post_response, product_schema)

        # Step 3: PUT - Full update
        print("\n3. Testing PUT - Full Update")
        update_payload = {
            "name": "Apple MacBook Pro 16 (Updated)",
            "data": {
                "year": 2023,
                "price": 2199.99,
                "CPU model": "M2 Max",
                "Hard disk size": "2 TB",
                "color": "Space Gray"
            }
        }
        put_response = self.api_client.put(
            self.get_full_url(f"objects/{object_id}"),
            json=update_payload
        )
        self.assert_status_code(put_response, 200)
        self.validate_response_schema(put_response, product_schema)
        updated_object = put_response.json()
        assert updated_object['data']['Hard disk size'] == "2 TB", "Full update failed"

        # Step 4: PATCH - Partial update
        print("\n4. Testing PATCH - Partial Update")
        patch_payload = {
            "data": {
                "price": 2099.99,
                "color": "Silver"
            }
        }
        patch_response = self.api_client.patch(
            self.get_full_url(f"objects/{object_id}"),
            json=patch_payload
        )
        self.assert_status_code(patch_response, 200)
        self.validate_response_schema(patch_response, product_schema)
        patched_object = patch_response.json()
        assert patched_object['data']['color'] == "Silver", "Partial update failed"

        # Step 5: Verify GET single object
        print("\n5. Testing GET - Verify Updated Object")
        get_response = self.api_client.get(self.get_full_url(f"objects/{object_id}"))
        self.assert_status_code(get_response, 200)
        self.validate_response_schema(get_response, product_schema)
        retrieved_object = get_response.json()
        assert retrieved_object['data']['price'] == 2099.99, "Object not updated correctly"

        # Step 6: DELETE
        print("\n6. Testing DELETE")
        delete_response = self.api_client.delete(self.get_full_url(f"objects/{object_id}"))
        self.assert_status_code(delete_response, 200)

        # Step 7: Verify deletion
        print("\n7. Verifying Deletion")
        get_deleted_response = self.api_client.get(self.get_full_url(f"objects/{object_id}"))
        self.assert_status_code(get_deleted_response, 404)

        print("\nCRUD sequence completed successfully") 
