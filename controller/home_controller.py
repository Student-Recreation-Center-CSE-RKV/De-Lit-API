from fastapi import HTTPException
from models.home_model import BlockModel
from utilities.utils import client

# Initialize the MongoDB connection
mydb = client["Delit-test"]
connection = mydb.home


class GetAllBlocks:
    @staticmethod
    async def execute() -> list:
        """
        Retrieves all blocks.

        Returns:
            list: List of dictionaries, each representing a block.

        Raises:
            HTTPException: If no data is found in the database (404).
        """
        blocks = await connection.find().to_list(length=None)
        if not blocks:
            raise HTTPException(status_code=404, detail="Data not found in the database.")

        for block in blocks:
            block["_id"] = str(block["_id"])  # Convert ObjectId to string
        return blocks


class GetBlockByName:
    @staticmethod
    async def execute(block_name: str) -> dict:
        """
        Fetches a specific block by name.

        Args:
            block_name (str): Name of the block to retrieve.

        Returns:
            dict: Block data as dictionary.

        Raises:
            HTTPException: If block is not found (404).
        """
        result = await connection.find_one({"name": block_name.lower()})
        if not result:
            raise HTTPException(status_code=404, detail="Data not found in the database.")

        result["_id"] = str(result["_id"])
        return result


class UpdateBlock:
    @staticmethod
    async def execute(block_name: str, data: BlockModel) -> dict:
        """
        Updates a block by name.

        Args:
            block_name (str): The block to be updated.
            data (BlockModel): New data model for the block.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: If block is not found (404).
        """
        block = await connection.find_one({"name": block_name.lower()})
        if not block:
            raise HTTPException(status_code=404, detail="Data not found in the database.")

        updated_data = data.model_dump()
        await connection.update_one({"name": block_name.lower()}, {"$set": updated_data})
        return {"message": "Block updated successfully"}


class DeleteBlock:
    @staticmethod
    async def execute(block_name: str) -> dict:
        """
        Deletes a block by name.

        Args:
            block_name (str): The block to delete.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: If block is not found (404).
        """
        block = await connection.find_one({"name": block_name.lower()})
        if not block:
            raise HTTPException(
                status_code=404, detail="Data not found in the database.")

        await connection.delete_one({"name": block_name.lower()})
        return {"message": "Block deleted successfully"}


class CreateBlock:
    @staticmethod
    async def execute(data: BlockModel) -> dict:
        """
        Inserts a new block into the database.

        Args:
            data (BlockModel): The data for the new block.

        Returns:
            dict: Success message with the ID of the newly created block.

        Raises:
            HTTPException: If a block with the same name already exists.
        """
        # Check if the block name already exists
        existing_block = await connection.find_one({"name": data.name.lower()})
        if existing_block:
            raise HTTPException(status_code=400, detail="Block with this name already exists.")

        # Insert the new block
        new_block = data.model_dump()
        # Ensure the name is stored in lowercase
        new_block["name"] = new_block["name"].lower()
        result = await connection.insert_one(new_block)

        return {"message": "Block created successfully", "block_id": str(result.inserted_id)}
