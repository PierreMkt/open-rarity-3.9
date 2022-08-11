import logging

import numpy as np

from open_rarity.models.collection import Collection
from open_rarity.models.token import Token
from open_rarity.models.token_metadata import (
    AttributeName,
    StringAttributeValue,
)
from open_rarity.scoring.scorer import Scorer
from open_rarity.scoring.utils import get_attr_probs_weights

logger = logging.getLogger("open_rarity_logger")


class SumRarityScorer(Scorer):
    """sum of n trait probabilities"""

    def score_token(
        self, collection: Collection, token: Token, normalized: bool = True
    ) -> float:
        return self._score_token(collection, token, normalized)

    def score_tokens(
        self,
        collection: Collection,
        tokens: list[Token],
        normalized: bool = True,
    ) -> list[float]:
        # Memoize for performance
        collection_null_attributes = collection.extract_null_attributes()
        return [
            self._score_token(
                collection, t, normalized, collection_null_attributes
            )
            for t in tokens
        ]

    # Private methods
    def _score_token(
        self,
        collection: Collection,
        token: Token,
        normalized: bool = True,
        # If provided, will be used instead of re-calculating on @collection
        collection_null_attributes: dict[
            AttributeName, StringAttributeValue
        ] = None,
    ) -> float:
        logger.debug(f"Computing arithmetic mean for token {token}")

        attr_probs, attr_weights = get_attr_probs_weights(
            collection=collection,
            token=token,
            normalized=normalized,
            collection_null_attributes=collection_null_attributes,
        )

        return np.dot(attr_probs, attr_weights)