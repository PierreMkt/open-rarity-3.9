import numpy as np
from base import BaseRarityFormula
from utils import flatten_attrs, get_attr_probs

from openrarity.models.token import Token


class HarmonicMeanRarity(BaseRarityFormula):
    """harmonic mean of a token's n trait probabilities"""

    def score_token(self, token: Token) -> float:
        """calculate the score for a single token"""

        string_attr_list = flatten_attrs(token.metadata.string_attributes)
        attr_probs = get_attr_probs(string_attr_list, token)

        return np.mean(np.reciprocal(attr_probs)) ** -1
