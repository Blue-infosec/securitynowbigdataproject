var sockjs = require('sockjs'),
    redis = require('redis'),
    express = require('express'),
    app = express(),
    fs = require('fs'),
    os = require('os'),
    http = require('http'),
    https = require('https'),
    crypto = require('crypto'),
    paths = require('path'),
    cluster = require('cluster'),
    lactate = require('lactate'),
    memoize = require('memoizee'),
    memwatch = require('memwatch'),
    connect = require('connect'),
    jade = require('jade'),
    cons = require('consolidate'),
    compression = require('compression')(),
    session = require('express-session'),
    bodyParser = require('body-parser'),
    cookieParser = require('cookie-parser'),
    port = 8065, mongo = require('mongodb').MongoClient,
    spawn = require('child_process').spawn,
    exec = require('child_process').exec,
    program = require('commander'), collection,
    format = require('util').format;


memwatch.on('leak', function (info) {

    console.log("MEMORY LEAK DATA: ", info);

});

memwatch.on('stats', function (stats) {

    console.log("HEAP USAGE STATS: ", stats);

});

var instances = 1;//os.cpus().length;

if (cluster.isMaster) { // fork worker threads
    for (var i = 0; i < instances; i += 1) {
        console.log('Starting worker thread #' + i);
        worker = cluster.fork();

    }

    worker.on('death', function (worker) {
        // Log deaths!
        console.log(': worker ' + worker.pid + ' died.');
        // If autoRestart is true, spin up another to replace it
        if (this.autoRestart) {
            console.log(': Restarting worker thread...');
            cluster.fork();
        }
    });
} else {


    function calldocker(cmd, name) {


        if (0 == cmd.length){
            cmd = ['/bin/bash'];
        }


        exec('docker inspect ' + name, function (err, stdout) {
            if (err) throw err;

            var obj = JSON.parse(stdout);
            var id = obj[0].ID;
            var proc = spawn('lxc-attach', ['-n', id].concat(cmd), { stdio: 'inherit' });
        });
    }

    app.use(express.static(__dirname + '/public'));
    app.use(bodyParser());

    app.use(cookieParser());
    app.use(session({ secret: 'chessfrombrains', cookie: { maxAge: 60000 }}));

    app.engine('jade', cons.jade);
    app.set('view engine', 'jade');
    app.set('views', __dirname + '/views');


    var index = fs.readFileSync(__dirname + '/public/index.html');
    fs.watchFile(__dirname + '/public/index.html', function (curr, prev) {
        console.log("RELOADING INDEX.HTML!!!!!");
        index = fs.readFileSync(__dirname + '/public/index.html');
    });

    app.all('/', function (req, res) {
        res.set('Content-Type', 'text/html');
        res.send(index);
        console.log("/ HEADERS: ", req.headers['user-agent']);
    });

    mongo.connect('mongodb://172.17.0.5:27017/twapp_storage', function(err, db) {
        if(err) throw err;

        collection = db.collection('posts');

        collection.find("security",{fields: {Data: 1}}).toArray(function(err, docs) {
            console.log("Returned #" + docs.length + " documents");
        });

        app.get('/fullset', function(req, res){
            console.log("SOMEONE's Browser is about to get Really sluggish!");
            console.log("/ HEADERS: ", req.headers['user-agent']);
            collection.find().toArray(function(err, docs) {
                console.log("Returned #" + docs.length + " documents");
                res.send(docs);
            });
        });

        app.get('/episode/:num', function(req, res){
            console.log("/ HEADERS: ", req.headers['user-agent']);
            console.log("CONNECTION FROM: ", req.headers)
            collection.find({ episode: req.params['num'] } ).toArray(function(err, docs) {
                console.log("Returned #" + docs.length + " Epidsode based documents");
                res.send(docs);
            });
        });

        app.get('/search/:val', function(req, res){
            console.log("/ HEADERS: ", req.headers['user-agent']);
            console.log("CONNECTION FROM: ", req.headers)
            console.log("QUERY VALUES: ", req.params['val']);
            collection.find({ original: {"$regex": req.params['val'] }} ).toArray(function(err, docs) {
                console.log("Returned #" + docs.length + " Epidsode based documents");
                res.send(docs);
            });
        });
    });


    console.log("PORT HTTP: ", port);

    app.listen(port);
}