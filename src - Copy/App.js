//projectID, userName, userSecret
import React, { Component } from "react";
//import ChatFeed from './components/ChatFeed';
import HomePage from './HomePage';
import ReactDOM from 'react-dom';
import './App.css';

class App extends Component {
	constructor(props){
		super(props);
	}

	render() {
		return (
			<div>
				<HomePage />
			</div>
		
		)
	}
}

export default App;

ReactDOM.render(<App />, document.getElementById('root'));






// const App = () => {
// 	return (
// 		<ChatEngine
// 			height="100vh"
// 			projectID="f23ddd8f-235c-4ee0-a70a-e61b144b90ac"
// 			userName="joshryuzaki@gmail.com"
// 			userSecret="123456"
// 			renderChatFeed={(chatAppProps) => <ChatFeed {... chatAppProps}/>}
// 			/>
// 		);
// }

// export default App;
