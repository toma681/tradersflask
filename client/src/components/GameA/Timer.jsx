import React, { useState, useEffect } from 'react';
import { Box, Flex, Progress, Text } from '@chakra-ui/react';
// SRC: https://codesandbox.io/s/chakra-ui-progress-countdown-7fszj?file=/src/Content.js:165-600

function useCountdown(mins, onTimeOut) {
	const [secs, decrement] = useState(mins * 60);
	const [progress, increment] = useState(0);
	useEffect(() => {
		if (secs > 0) {
			const progressLevel = setInterval(() => {
				increment(progress + 100 / (mins * 60));
				decrement(secs - 1);
			}, 1000);
			return () => clearInterval(progressLevel);
		} else {
			return onTimeOut();
		}
	}, [progress, secs, mins]);
	const sec = parseInt(secs % 60, 10);
	const seconds = sec < 10 ? '0' + sec : sec;
	return [progress, seconds];
}

export function Timer({ onTimeOut, time }) {
	const [progress, seconds] = useCountdown(time, onTimeOut);

	return (
		<Box
			borderColor="gray.200"
			borderWidth="1px"
			rounded="md"
			bg="white"
			p={[1, 4]}
			w="100%"
		>
			<Text>Time Remaining</Text>
			<Flex flexDirection="row" width="100%" alignItems="center">
				<Progress value={progress} height="2px" w="90%" grow={1} />
				<Text ml="auto">{`${seconds} s`}</Text>
			</Flex>
		</Box>
	);
}
