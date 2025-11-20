"""Compute PCA decomposition and component projections"""

##
# Imports

import modal
import typer

import astrocytes.backend.pca as backend
from astrocytes.backend.pca import (
    app as embed_app,
    ImageEmbedder
)



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