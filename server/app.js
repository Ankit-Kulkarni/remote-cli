var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var index = require('./routes/index');
var users = require('./routes/users');

var app = express();

var http = require('http').Server(app);
var io = require('socket.io')(http);

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use('/static', express.static(path.join(__dirname, 'public')));

app.use('/', index);
app.use('/users', users);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});


// ***************************************************************

// application remote-cli code start 
var clients_to_socket = {};
var socket_to_client = {};
var client_info = {};

io.on('connection', function(socket){

  console.info('A user connected with socket id = ' + socket.id );
  

  // Getting client payload for identification of client 
  socket.on("connect_client", function(cl_info){
       client_info[cl_info.client_id] = cl_info;
       client_info[cl_info.client_id]["socket"] = socket.id;
       console.log("Client info is while connecting is -")
       console.log(client_info);
       client_id = cl_info.client_id;
       clients_to_socket[client_id] = socket.id;
       socket_to_client[socket.id] = client_id;
       io.emit("live_client_list", client_info );
       // console.log(clients_to_socket);
  });

  socket.on("get_client_list", function(){
    console.log("socket id in get cleint list is" + socket.id );
    console.log("client info is ");
    io.to(socket.id).emit("live_client_list", client_info);
  })

  // Clear client from global array on disconnect 
  socket.on('disconnect', function(){
      console.log('user disconnected');
      client_id = socket_to_client[socket.id];
      delete client_info[client_id];
      delete socket_to_client[socket.id];
      delete clients_to_socket[client_id];
      console.log("client info while disconnecting ");
      console.log(client_info);
      io.emit("live_client_list", client_info);
    });

  // 
  socket.on('chat message', function(msg){
      console.log('message: ' + msg);
      io.emit('chat message', msg);
    });

  socket.on('command', function(msg, room){
      console.log('message: ' + msg);
      io.to(room).emit('command', msg);
    });

  socket.on("handshake", function(roomId){
    console.log("got into handshake process for room " + roomId);
    requestClientId = socket.id;
    io.to(roomId).emit("handshake", roomId, requestClientId);
  });

  socket.on("command-output", function(op, roomId){
    io.to(roomId).emit("show_command_op", op);
  });

});
module.exports = app;
http.listen(4000, function(){
	  console.log('listening on localhost:4000');
});

