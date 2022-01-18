import React, { useState } from 'react';

import GameB from '../../pages/GameB';

import { Button, Stack, NumberInput, NumberInputField } from '@chakra-ui/react';

/**
 * @param maximum - previous spread high
 * @param minimum - previous spread low
 * @returns interace to submit new spread
 */

const SetSpreadUI = ({ minimum, maximum, action }) => {
	const [submit, submitRegister] = useState(false);

	let disp;

	if (submit) {
		disp = <GameB />;
	}

	return (
		<Stack spacing={4} direction="column" align="center" margin="10px">
			<text>
				<b>Set New Spread</b>
			</text>
			<text>Input Low</text>
			<NumberInput
				defaultValue={100}
				min={minimum}
				width="200px"
				allowMouseWheel="true"
			>
				<NumberInputField />
			</NumberInput>
			<text>Input High</text>
			<NumberInput
				defaultValue={100}
				max={maximum}
				width="200px"
				allowMouseWheel="true"
			>
				<NumberInputField />
			</NumberInput>
			<Button onClick={() => submitRegister()}>Submit</Button>
			{disp}
		</Stack>
	);
};

export default SetSpreadUI;
