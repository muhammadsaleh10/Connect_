import { NewMessageForm } from "react-chat-engine";

const MyMsgForm = (props) => {
	return (
		<div id="my-message-form-id">
			<NewMessageForm {...props} />
		</div>
		
	)
}

export default MyMsgForm;
