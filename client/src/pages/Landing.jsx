import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

import { Flex, Spacer, Button, Text, Heading, Input } from '@chakra-ui/react';

import Logo from '../img/logo-white.png';
// import Goldman from '../img/sponsors/goldman.png';
import Sig from '../img/sponsors/sig.png';
import Citadel from '../img/sponsors/citadel.png';
import Optiver from '../img/sponsors/optiver.png';
import Flow from '../img/sponsors/flow.png';

import styles from '../styles/landing.module.scss';
import classnames from 'classnames';

const Landing = () => {
	const [username, setUsername] = useState('');
	const [error, setError] = useState('');

	const verifyUsername = async () => {
		if (!username) {
			setError('Please enter your email to continue!');
			return false;
		}
		setError('');
		return true;
	};

	const submit = async () => {
		console.log(username);
		await axios
			.post('http://127.0.0.1:5000/users/registerUser', { username })
			.then((res) => {
				var stringRes = JSON.stringify(res['data']);
				// console.log("res: " + stringRes);
				document.cookie = 'userHash=' + stringRes;
				// console.log("cookie: " + getCookie("userHash"));
			});
	};

	function getCookie(cname) {
		var name = cname + '=';
		var decodedCookie = decodeURIComponent(document.cookie);
		var ca = decodedCookie.split(';');
		for (var i = 0; i < ca.length; i++) {
			var c = ca[i];
			while (c.charAt(0) == ' ') {
				c = c.substring(1);
			}
			if (c.indexOf(name) == 0) {
				return c.substring(name.length, c.length);
			}
		}
		return '';
	}

	return (
		<>
			<Flex
				direction="column"
				justify="center"
				align="center"
				h="85vh"
				className={styles['bg']}
			>
				<img src={Logo} alt="Traders at Berkeley" />
				<a
					href="https://traders.berkeley.edu/"
					target="_blank"
					rel="noreferrer"
				>
					<Heading as="h1" color="white" size="3xl" mt="3rem">
						Traders at Berkeley
					</Heading>
				</a>
				<Heading as="h3" color="white" size="xl" my="1rem">
					West Coast Trading Competition
				</Heading>

				{/* <Input
					w="50%"
					bg="white"
					value={username}
					onChange={(e) => setUsername(e.target.value)}
					placeholder="Enter your email."
				/>

				<Text color="red" mt="1rem">
					{error}
				</Text> */}

				<Flex mt="2.5rem" w="50%">
					<Link
						to={() => verifyUsername() && '/game-a'}
						className={styles['button']}
					>
						<Button size="lg" w="100%">
							Game A
						</Button>
					</Link>
					<Spacer />
					<Link
						to={() => verifyUsername() && '/game-b'}
						className={styles['button']}
					>
						<Button size="lg" w="100%" onClick={submit}>
							Game B
						</Button>
					</Link>
				</Flex>
			</Flex>

			{/* <Flex direction="column" align="center" h="40vh">
				<Heading as="h5" color="black" size="xl" my="2rem">
					Sponsored By:
				</Heading>
				<Flex align="center">
					<img
						src={Sig}
						alt="SIG"
						className={classnames(styles['sponsor'], styles['sig'])}
					/>
					<img
						src={Citadel}
						alt="Citadel"
						className={classnames(styles['sponsor'], styles['citadel'])}
					/>
				</Flex>
				<Flex mt="2rem" align="center">
					<img
						src={Optiver}
						alt="Optiver"
						className={classnames(styles['sponsor'], styles['optiver'])}
					/>
					<img
						src={Flow}
						alt="Flow Traders"
						className={classnames(styles['sponsor'], styles['flow'])}
					/>
				</Flex> */}
			{/* <Text mt="3.5rem" pb="1rem">
					Traders at Berkeley 2021
				</Text>
			</Flex> */}
		</>
	);
};

export default Landing;
