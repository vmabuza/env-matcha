document.addEventListener('DOMContentLoaded',() => {

	
	var socket = io.connect(`http://${document.domain}:${location.port}`);
	// socket.on( 'connect', () => {
		
		// } )
	let user_name =username;
	let room = user_name;
	joinRoom(room)


	Notification
	socket.on( 'Notification',  msg => {
		console.log(msg)

		var val = parseInt($('#notification').find('.badge').text());
		
		$('#notification').find('.badge').text(val + 1)

	})

	//Join room
	function joinRoom(room){
		socket.emit('join',{'user_name':user_name,'room':room})

		// document.querySelector('.message_holder').innerHTML=''
	}

	//Print system message
	// function printSysMsg(msg){
	// 	const p = document.createElement('p')
	// 	p.innerHTML = msg;
	// 	document.querySelector('.message_holder').append(p)

	// }
					
					
})