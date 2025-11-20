"""Common analysis routines"""

##
# Imports

import atdata

from dataclasses import dataclass

from typing import (
    AsyncIterable,
    AsyncGenerator,
    #
    Type,
    Generic,
    TypeVar,
    TypeAlias,
    Literal,
)
T = TypeVar( 'T' )
ST = TypeVar( 'ST', bound = atdata.PackableSample )


##
# Remote data management

WDSExtension: TypeAlias = Literal[
    '.tar',
    '.tar.gz',
]

@dataclass
class RemoteData:
    """TODO"""
    ##
    stem: str
    """TODO"""
    shard_ids: list[int]
    """TODO"""
    #
    extension: WDSExtension = '.tar'
    """TODO"""
    digits: int = 6
    "TODO"

    ## Helpers

    def as_atdata( self, sample_type: Type[ST] ) -> atdata.Dataset[ST]:
        """TODO"""
        return atdata.Dataset[sample_type]( self.wds_url )

    @property
    def wds_url( self ) -> str:
        """TODO"""
        if len( self.shard_ids ) < 1:
            raise ValueError( 'Cannot form WDS URL: shard list is empty' )

        number_pattern = f'%0{self.digits:1d}d'

        if len( self.shard_ids ) == 1:
            shard_pattern = f'{self.stem}-{number_pattern}'
            return shard_pattern.format( self.shard_ids[0] )

        shards_sorted = list( sorted( self.shard_ids ) )
        low_shard, high_shard = shards_sorted[0], shards_sorted[-1]
        
        # Make sure shards are purely sequential
        # TODO Handle this more gracefully
        for s_prev, s in zip( shards_sorted[:-1], shards_sorted[1:] ):
            if s != s_prev + 1:
                raise ValueError( f'Cannot form WDS URL: shard_ids not sequential {s_prev} -> {s}' )

        shard_pattern = (
            f'{self.stem}-'
            + '{'
            + '{low_id}..{high_id}'.format(
                low_id = number_pattern % low_shard,
                high_id = number_pattern % high_shard
            )
            + '}'
            + self.extension
        )
        return shard_pattern


##
# Helper functions

async def aenumerate( asequence: AsyncIterable[T], start: int = 0 ):
    """
    Asynchronously enumerate an async iterator from a given start value.
    """
    n = start
    async for elem in asequence:
        yield (n, elem)
        n += 1


#