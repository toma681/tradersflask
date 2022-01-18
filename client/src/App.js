import React from 'react';

import Landing from './pages/Landing';
import GameA from './pages/GameA';
import GameB from './pages/GameB';

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

const App = () => {
	return (
		<Router>
			<Switch>
				{/* <Route exact path="/index.html">
					<Landinkg />
				</Route> */}
				<Route path="/game-a">
					<GameA />
				</Route>
				<Route path="/game-b">
					<GameB />
				</Route>
				<Route path="/">
					<Landing />
				</Route>
			</Switch>
		</Router>
	);
};

export default App;
