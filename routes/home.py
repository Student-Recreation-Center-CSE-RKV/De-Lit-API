from fastapi import APIRouter, HTTPException
from models.home_model import BlockModel
from controller.home_controller import GetAllBlocks, GetBlockByName, UpdateBlock, DeleteBlock ,CreateBlock
from utilities.utils import handle_exception
app = APIRouter(tags=['Home'])

@app.get("/", response_model=list, summary="Fetch all homepage blocks")
@handle_exception
async def get_all_blocks() -> list:
    """
    Retrieves all blocks on the homepage.

    Returns:
        list: List of blocks with data fields: name, content, image_link.

    Raises:
        HTTPException: If no data is found (404).
    """
    return await GetAllBlocks.execute()


@app.get("/{block_name}", response_model=dict, summary="Fetch specific block data")
@handle_exception
async def get_block_data(block_name: str) -> dict:
    """
    Retrieves a specific block by its name.

    Args:
        block_name (str): Name of the block to retrieve.

    Returns:
        dict: Block data (name, content, image_link).

    Raises:
        HTTPException: If block data is not found (404).
    """
    return await GetBlockByName.execute(block_name)


@app.put("/{block_name}", response_model=dict, summary="Update a specific block")
@handle_exception
async def update_block(block_name: str, data: BlockModel) -> dict:
    """
    Updates a block's data by its name.

    Args:
        block_name (str): The block to be updated.
        data (BlockModel): New data for the block.

    Returns:
        dict: Success message if the block is updated.

    Raises:
        HTTPException: If the block is not found (404).
    """
    return await UpdateBlock.execute(block_name, data)


@app.delete("/{block_name}", response_model=dict, summary="Delete a specific block")
@handle_exception
async def delete_block(block_name: str) -> dict:
    """
    Deletes a specific block by its name.

    Args:
        block_name (str): The block to delete.

    Returns:
        dict: Success message if deletion is successful.

    Raises:
        HTTPException: If block is not found (404).
    """
    return await DeleteBlock.execute(block_name)


@app.post("/", response_model=dict, summary="Create a new block")
@handle_exception
async def create_block(data: BlockModel) -> dict:
    """
    Creates a new block.

    Args:
        data (BlockModel): The data for the new block.

    Returns:
        dict: Success message with the ID of the newly created block.

    Raises:
        HTTPException: If a block with the same name already exists.
    """
    return await CreateBlock.execute(data) 