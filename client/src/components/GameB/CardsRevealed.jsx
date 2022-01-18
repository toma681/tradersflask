import React from 'react';

import { Text } from '@chakra-ui/react';

/**
 * @param cardsRevealed - list of cards revealed from backend
 * @returns text string of cards that have been revealed
 */
const CardsRevealed = ({ cardsRevealed }) => {
	return (
		<Text>
			<b>Cards Revealed:</b> {{ cardsRevealed }}
		</Text>
	);
};

export default CardsRevealed;
