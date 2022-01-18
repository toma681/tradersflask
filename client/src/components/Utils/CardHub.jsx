import React from 'react';

import {
	Flex,
	Text,
	Heading,
	Box,
	Grid,
	Button,
	ListItem,
	UnorderedList,
} from '@chakra-ui/react';

/**
 * @param {map[gameID: players[]]} available_games: Map of game IDs to
 * @param {string} game: Name of the game
 * @returns A single card of given type
 * @todo get names from backend
 */
export const CardHub = ({ available_games, game }) => {
	return (
		<Box borderWidth="1px" borderRadius="lg" w="auto">
			<Flex flexDir="column" alignItems="center">
				<Heading style={{ 'text-align': 'center' }}>{game}</Heading>
				<Text
					size="xx-large"
					style={{ 'text-align': 'center', margin: '10px' }}
				>
					{' '}
					Join a Game{' '}
				</Text>
				<Grid templateColumns="repeat(3, 1fr)" gap={6} margin="20px">
					{available_games.map((game, ind) => (
						<Flex flexDir="column">
							<Button onClick={() => alert(game[0])}>
								Join Game {ind + 1}
							</Button>
							<UnorderedList>
								{game[1].map((name) => (
									<ListItem>{name}</ListItem>
								))}
							</UnorderedList>
						</Flex>
					))}
				</Grid>
			</Flex>
		</Box>
	);
};
