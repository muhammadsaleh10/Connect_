import React, { Component } from "react";
import { useState, useEffect } from 'react';
import { ChatEngine, ChatList, ChatFeed, getOrCreateChat } from 'react-chat-engine';
import { useParams } from "react-router-dom";
//import ChatFeed from "./components/ChatFeed";
import MyMsgForm from "./components/MyMsgForm";


const withRouter = WrappedComponent => props => {
	const params = useParams();
	// etc... other react-router-dom v6 hooks
  
	return (
	  <WrappedComponent
		{...props}
		params={params}
		// etc...
	  />
	);
  };


//		const [username, setUsername] = useState('');

function createDirectChat(creds, username, setUsername) {
	getOrCreateChat(
		creds,
		{ is_direct_chat: true, usernames: [username] },
		() => setUsername('')
	);
}

function renderChatForm(creds, username, setUsername) {
	return (
		<div>
			<input
				placeholder='Username' 
				value={username}
				onChange={(e) => setUsername(e.target.value)}
			/>
			<button onClick={() => {
									createDirectChat(creds, username, setUsername); window.location.reload();
									
									}
							}>
				Create
			</button>
		</div>
	)
}

function display(devicePlatform,resp, userName, username, setUsername){
	if(!resp) {
				return <div>
						<div>
							<p>Loading...</p>
						</div>
					</div>}
	else if(resp.length == 0) {
		var vartag = (
			<div>
			<div id="_device_platform"><p>{devicePlatform}</p></div>
			<ChatEngine
			height='100vh'
			userName={userName}
			userSecret='123456-dummy'
			projectID='PID'
			renderNewChatForm={(creds) => renderChatForm(creds, username, setUsername)}
			renderNewMessageForm = { (messageFormProps) => <MyMsgForm {...messageFormProps} /> }
			renderChatFeed={(chatAppProps) => <ChatList {...chatAppProps} />} //swap chat list and chat feed
			renderChatList={(chatAppProps) => <ChatFeed {...chatAppProps} />}
			/>
			</div>
			)
			//console.log(vartag);
			return vartag
		}
		else {
			var vartag = (
				<div>
				<div id="_device_platform"><p>{devicePlatform}</p></div>
				<ChatEngine
				height='100vh'
				userName={userName}
				userSecret='123456-dummy'
				projectID='PID'
				renderNewChatForm={(creds) => renderChatForm(creds)}
				renderNewMessageForm = { (messageFormProps) => <MyMsgForm {...messageFormProps} /> }
				// renderChatFeed={(chatAppProps) => <ChatList {...chatAppProps} />} //swap chat list and chat feed
				// renderChatList={(chatAppProps) => <ChatFeed {...chatAppProps} />}
			/>
			</div>
			)
			
			//console.log(vartag);
			return vartag
		}
}


function UserPage (props) {
	const [resp, setResponse] = useState(null);
	const [username, setUsername] = useState('');
	var userName = props.params.userName;//went through stress trying to fix this, was this.props.params.match, along with something else in HomePage.js
	var devicePlatform = props.params.devicePlatform;


	var url = "https://api.chatengine.io/chats/";
	var myHeaders = new Headers();
	myHeaders.append("Project-ID", "PID");
	myHeaders.append("User-Name", userName);
	myHeaders.append("User-Secret", "123456-dummy");

	var requestOptions = {
		method: 'GET',
		headers: myHeaders,
		redirect: 'follow'
		};

	useEffect(() => {
		fetch(url, requestOptions)
		.then(response => response.json())
		.then(res => setResponse(res))
	}, []);
	var dis = display(devicePlatform,resp, userName, username, setUsername);
	return dis
	
	
	
	
}

UserPage = withRouter(UserPage);
export default UserPage; //need to use withRouter for this react version to work

