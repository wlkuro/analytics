import { Router } from "express"

var exec = require('child_process').exec;


const router = Router()

//const base = [
//  { name: 'とろ', price: 300 },
//  { name: 'いか', price: 200 },
//  { name: 'かっぱ巻き', price: 100 }
//]
var base = {};

/* GET users listing. */
router.get("/base", (req, res) => {
  var child = exec("python _ganalytics.py "+req.query.url, function (error, stdout, stderr) {
    console.log('stdout: ' + stdout);
    console.log('stderr: ' + stderr);
    if (error !== null ){
      console.log('exec error: ' + error);
    }
    res.header('Content-Type', 'application/json; charset=utf-8');
    res.send(stdout);
//    base = stdout;
//    res.json(stdout)
  });


//    res.json(base)
})

export default router
