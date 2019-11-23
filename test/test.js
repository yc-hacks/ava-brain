var https = require("http");
function httpGet2() {
  console.log("In function");
  var question = "What are we";
  var options = {
    method: "GET",
    hostname: "ec2-54-86-61-234.compute-1.amazonaws.com",
    path: "/ask?question=What%are",
    headers: {}
  };
  var req = https.request(options, function(res) {
    var chunks = [];
    console.log("Waiting...");
    res.on("data", function(chunk) {
      chunks.push(chunk);
    });
    res.on("end", function(chunk) {
      var body = Buffer.concat(chunks);
      console.log(body.toString());
    });
    res.on("error", function(error) {
      console.error(error);
    });
  });
  req.end();
}
const response = await httpGet2();
