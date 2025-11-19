"""Embed images"""

##
# Imports

import modal
import typer
import asyncio

import atdata
import astrocytes

from toile.schema import Frame

from ._common import (
    aenumerate,
    RemoteData,
)

import astrocytes.backend.embed as backend
from astrocytes.backend.embed import (
    app as embed_app,
    ImageEmbedder
)

from typing import (
    Type,
    TypeAlias,
    Literal,
)


##
# ...

async def embed_parallel(
            image_data: RemoteData,
            output_stem: str,
            **kwargs,
        ) -> RemoteData:
    """
    TODO
    """

    assert embed_app.name is not None, \
        'Embedding backend modal app has no name'

    # Get the embedding class interface for the Modal backend
    
    _Embedder = modal.Cls.from_name( embed_app.name, 'ImageEmbedder' )
    embedder = _Embedder()

    # Create the arguments for parallel execution

    dataset = image_data.as_atdata( Frame )

    process_kwargs = dict(
        batch_size = 256,
        n_batches = None,
        kind = 'Frame',
        sharded = False,
        verbose = True,
    )
    process_kwargs.update( kwargs )

    process_args = [
        (s, f'{output_stem}-{i:06d}')
        for i, s in enumerate( dataset.shard_list )
    ]

    # Run it!

    dataset_results = {
        process_args[i][0]: result
        async for i, result in aenumerate(
            embedder.process.starmap(
                process_args,
                kwargs = process_kwargs,
                return_exceptions = True,
                wrap_returned_exceptions = False,
            )
        )
    }

    # Package return value
    result_stem = None
    result_shard_ids = []
    for _, output_shard in dataset_results.items():

        if isinstance( output_shard, Exception ):
            result_shard_ids.append( None )
            continue
        
        assert isinstance( output_shard, str )

        if result_stem is None:
            # Pull off last component (e.g., '-000002.tar')
            result_stem = '-'.join( output_shard.split( '-' )[:-1] )

        result_shard_ids.append(
            int( output_shard.split( '-' )[-1].split( '.' )[0] )
        )       
    
    assert result_stem is not None, \
        'Returned embedding results were empty'
                    
    ret = RemoteData(
        stem = result_stem,
        shard_ids = result_shard_ids,
        digits = 6,
    )
    return ret


##
# Typer command entrypoint

cli_app = typer.Typer()

BuiltinData: TypeAlias = Literal[
    'bath_application',
    'uncaging',
]

@cli_app.command( name = 'parallel' )
def _cli_parallel(
            oa: BuiltinData | None = None,
            wds: str | None = None,
            output: str | None = None,
            #
            batch_size: int = 256,
            n_batches: int = -1,
            verbose: bool = False,
        ):
    """TODO"""

    # Normalize argsw

    if oa is not None:

        if oa == 'bath_application':
            at_ds = astrocytes.data.bath_application
        elif oa == 'uncaging':
            at_ds = astrocytes.data.uncaging
        
        assert at_ds is not None, \
            f'Unable to get OpenAstrocytes manifest for "{oa}"'
        
        wds = at_ds.url
    
    if wds is None:
        raise NotImplementedError( 'Backend-local data input not yet implemented.' )

    input_dataset = atdata.Dataset[Frame]( wds )
    input_stem = '-'.join( input_dataset.shard_list[0].split( '-' )[:-1] )

    if output is None:
        output = input_stem + '-embeddings'

    if n_batches < -1 or n_batches == 0:
        raise ValueError( f'Invalid `n_batches`: {n_batches}' )
    if n_batches == -1:
        n_batches_use = None
    else:
        n_batches_use = n_batches

    # Collate input

    input_shard_ids = [ int( s.split( '-' )[-1].split( '.' )[0] )
                        for s in input_dataset.shard_list ]
    input_data = RemoteData(
        stem = input_stem,
        shard_ids = input_shard_ids
    )

    # Execute

    output_data = asyncio.run(
        embed_parallel( input_data, output,
            batch_size = batch_size,
            n_batches = n_batches_use,
            verbose = verbose,
        )
    )

def main():
    cli_app()

if __name__ == '__main__':
    main()


#