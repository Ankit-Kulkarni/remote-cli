var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get("/client-list", function(req, res, next){
	res.render("clients", {title: 'Remote Terminal Access | Clients'} );
});

router.get("/terminal/:id", function(req, res, next){
	var terminalid = req.params.id;
	res.render("terminal", {title: "Client Terminal"});
});


module.exports = router;
