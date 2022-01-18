// SRC: https://github.com/amandeepmittal/blog-examples/blob/master/react/loginform-chakra-ui-complete/src/pages/Login.js
import React, { useState } from 'react';
import {
    Flex,
    Box,
    Heading,
    FormControl,
    FormLabel,
    Input,
    Button,
    CircularProgress,
    Text
} from '@chakra-ui/react';

// Firebase App (the core Firebase SDK) is always required and
// must be listed before other Firebase SDKs
import firebase from "firebase/app";

// Add the Firebase services that you want to use
import "firebase/auth";

var firebaseConfig = {
    apiKey: "AIzaSyD9kggrNFpwt3c1MYLuz8hVsQYswSACysQ",
    authDomain: "berkeley-trading-competition.firebaseapp.com",
    projectId: "berkeley-trading-competition",
    storageBucket: "berkeley-trading-competition.appspot.com",
    messagingSenderId: "141198621816",
    appId: "1:141198621816:web:f3e8515652099d56fd418d",
    measurementId: "G-E9DYCZ6HRG"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// firebase.auth().createUserWithEmailAndPassword(email, password)
//     .then((userCredential) => {
//         // Signed in 
//         var user = userCredential.user;
//         // ...
//     })
//     .catch((error) => {
//         var errorCode = error.code;
//         var errorMessage = error.message;
//         // ..
//     });

export function Login() {
    var cookie = document.cookie.split(";").find((elem) => elem.includes("@"))
    var un = document.cookie.split(";").find((elem) => elem.includes("#"))
    const [isSignedUp, setIsSignedUp] = useState(cookie === undefined);
    const [email, setEmail] = useState(isSignedUp ? cookie : "");
    const [username, setUsername] = useState(isSignedUp ? un : "");
    const [password, setPassword] = useState("");
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);


    const handleSignUp = async event => {
        event.preventDefault();

        setIsLoading(true);
        alert(username, email)

        firebase.auth().createUserWithEmailAndPassword(email, password)
            .then((userCredential) => {
                // Signed in 
                // SEND USERNAME TO DATABASE WITH EMAIL
                var user = userCredential.user;
                setIsSignedUp(true);
                setIsLoading(false);
                console.log(email + "; #" + username);
                document.cookie = email + "; #" + username + "; ";
            })
            .catch((error) => {
                var errorCode = error.code;
                console.log(errorCode);
                var errorMessage = error.message;
                setError(errorMessage);
                setIsLoading(false);
                setEmail('');
                setPassword('');
            });

    };

    const handleSignIn = async event => {
        event.preventDefault();

        setIsLoading(true);

        firebase.auth().signInWithEmailLink(email)
        try {
            //   await userLogin({ email, username });
            setIsSignedUp(true);
            setIsLoading(false);
            console.log(email + "; #" + username);
            document.cookie = email + "; #" + username;
        } catch (error) {
            setError('Invalid email. Please sign in with the email you registered with.');
            setIsLoading(false);
            setEmail('');
        }
    };

    return (
        <Flex width="full" align="center" justifyContent="center" >
            <Box
                p={8}
                maxWidth="500px"
                borderWidth={1}
                borderRadius={8}
                boxShadow="lg"
                background="white"
            >
                {isSignedUp ? (
                    <Box textAlign="center">
                        {/* <Text>{username} Logged in!</Text>
                        <Button
                            variantColor="orange"
                            variant="outline"
                            width="full"
                            mt={4}
                            onClick={() => setIsSignedUp(false)}
                        >
                            Sign out
                        </Button> */}
                        <Box textAlign="center" margin="10px">
                            <Heading>Sign Up</Heading>
                        </Box>
                        <form onSubmit={handleSignUp}>
                            <FormControl isRequired>
                                <FormLabel>Email</FormLabel>
                                <Input
                                    type="email"
                                    placeholder="Oski@berkeley.edu"
                                    size="lg"
                                    onChange={event => setEmail(event.currentTarget.value)}
                                />
                            </FormControl>
                            <FormControl isRequired>
                                <FormLabel>Password</FormLabel>
                                <Input
                                    type="password"
                                    placeholder="password123"
                                    size="lg"
                                    onChange={event => setPassword(event.currentTarget.value)}
                                />
                            </FormControl>
                            <Button
                                variantColor="teal"
                                variant="outline"
                                type="submit"
                                width="full"
                                mt={4}
                            >
                                {isLoading ? (
                                    <CircularProgress
                                        isIndeterminate
                                        size="24px"
                                        color="teal"
                                    />
                                ) : (
                                    'Sign Up'
                                )}
                            </Button>
                        </form>
                    </Box>
                ) : (
                    <>
                        <Box textAlign="center">
                            <Heading>Login</Heading>
                        </Box>
                        <Box my={4} textAlign="left">
                            <form onSubmit={handleSignIn}>
                                <FormControl isRequired>
                                    <FormLabel>Email</FormLabel>
                                    <Input
                                        type="email"
                                        placeholder="Oski@berkeley.edu"
                                        size="lg"
                                        onChange={event => setEmail(event.currentTarget.value)}
                                    />
                                </FormControl>
                                <FormControl isRequired>
                                    <FormLabel>Username</FormLabel>
                                    <Input
                                        placeholder="BigBear"
                                        size="lg"
                                        onChange={event => setUsername(event.currentTarget.value)}
                                    />
                                </FormControl>
                                <Button
                                    variantColor="teal"
                                    variant="outline"
                                    type="submit"
                                    width="full"
                                    mt={4}
                                >
                                    {isLoading ? (
                                        <CircularProgress
                                            isIndeterminate
                                            size="24px"
                                            color="teal"
                                        />
                                    ) : (
                                        'Sign In'
                                    )}
                                </Button>
                            </form>
                        </Box>
                    </>
                )}
            </Box>
        </Flex>
    );
}