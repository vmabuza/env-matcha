document.addEventListener('DOMContentLoaded',() => {

	
	var socket = io.connect(`http://${document.domain}:${location.port}`);
	// socket.on( 'connect', () => {
		
		// } )
	let user_name =document.getElementById("username").innerHTML;
	let room = user_name;
	let user
	joinRoom(room)

	var form = $( 'form' ).on( 'submit', e => {
		e.preventDefault()
		var d = new Date();
		var n = parseInt(d.getTime());
		

		
		let user_input = $( 'input.message' ).val()

		//Sending messages to the server
		socket.emit( 'my event', {
			time:n,
			user_name : user_name,
			message : user_input,
			room:user
		} )
		$( 'div.message_holder' ).append( `<div><b style="color: #000">${user_name}</b> ${user_input}</div>` )
		$( 'input.message' ).val( '' ).focus()

	} )
	
	socket.on('old',msg => {
		console.log(msg)
		const span_timestamp = document.createElement('span')
		span_timestamp.innerHTML = msg.time_stamp
		$( 'div.message_holder' ).append( `<div><b style="color: #000">${msg['user_name']}</b> ${msg.message}</div>` )
				
	})
	
	//Display incoming messages
	socket.on( 'my event',  msg => {

		const span_timestamp = document.createElement('span')
		span_timestamp.innerHTML = msg.time_stamp
		console.log(msg)
		console.log(Date())
		// $('div.message_holder').append(span_timestamp.innerHTML)
		$( 'div.message_holder' ).append( `<div><b style="color: #000">${msg['user_name']}</b> ${msg.message}</div>` )
		document.querySelector('.message_holder').scrollTop = document.querySelector('.message_holder').scrollHeight;
	})


	Notification
	socket.on( 'Notification',  msg => {
		const span_timestamp = document.createElement('span')
		span_timestamp.innerHTML = msg.time_stamp
		console.log(msg)
		console.log(Date())
		// $('div.message_holder').append(span_timestamp.innerHTML)
		$( 'div.message_holder' ).append( `<div><b style="color: #000">${msg['owner']}</b> has ${msg['id']} your profile</div>` )
		document.querySelector('.message_holder').scrollTop = document.querySelector('.message_holder').scrollHeight;
	})


	//Room selection
	document.querySelectorAll('.select-room').forEach(p =>{
		p.onclick = () =>{
			let newRoom = p.innerHTML;

			if(newRoom === user){
				msg = `You are already in ${room} room.`
				printSysMsg(msg)
			}else{

				// leaveRoom(room)
				// joinRoom(newRoom)
				user = newRoom
				document.getElementById('input').style = 'visible'
				document.getElementById('darker').style = 'visible'
			}

		}
	});
	//Leave room
	function leaveRoom(room){
		socket.emit('leave',{'user_name':user_name,'room':room})
	}

	//Join room
	function joinRoom(room){

		
		socket.emit('join',{'user_name':user_name,'room':room},)

		document.querySelector('.message_holder').innerHTML=''
	}

	//Print system message
	function printSysMsg(msg){
		const p = document.createElement('p')
		p.innerHTML = msg;
		document.querySelector('.message_holder').append(p)

	}
					
					
})
					
					

					
					
					
					
					
					
					
					
					// socket.on('disconnect', (reason) => {
						// 	console.log('Connection fell or your browser is closing.');
						// if (reason === 'io server disconnect') {
							//   // the disconnection was initiated by the server, you need to reconnect manually
							//   socket.connect();
							// }
							// else the socket will automatically try to reconnect
							//   });
							// socket.on('disconnect',() => {
								// 	socket.removeAllListeners('connect');
								// 	socket.removeAllListeners('my event');
								// 	socket.removeAllListeners('connection');
								// });
								
								
								
								
								
								
								
								
								
								
								
								
								//.val() is used to get input elements values in
								// jQuery, alternative in JS is .value.
								//The .val() method is primarily used to get the values 
								//of form elements such as input
								//.val() returns an array containing the value of each 
								//selected option.
								
								//   user = {
									// 	  user_name:user_name,
									// 	  message:user_input
									// 	}
									// 	fetch(`http://${document.domain}:${location.port}/message`,{
										// 		method:'POST',
										// 		mode:'cors',
										// 		headers:{'Content-Type':'application/json'},
										// 		body:JSON.stringify(user)
										// 	}).then(response =>{
											// 		if (response.status !== 200){
												// 			console.log(`Your Response is ${response.status} it wasn't 200`)
												
												// 			return;
												// 		}
												// 	}).then(response =>{
													// 		console.log(user)
													// 	})
													
													
													
													