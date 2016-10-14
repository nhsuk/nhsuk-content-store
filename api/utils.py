def get_block_representation(block, value, context):
    """
    Calls block.to_api_representation(...) if the block
    defines the method,
    falls back to block.get_prep_value(...) otherwise.
    """
    if hasattr(block, 'to_api_representation'):
        return block.to_api_representation(value, context)
    return block.get_prep_value(value)
