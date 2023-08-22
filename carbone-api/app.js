const fs = require('fs');
const carbone = require('carbone');
const express = require('express');
const Prometheus = require('prom-client')
const app = express();
const PORT = process.env.PORT || 3002
const SERVER = process.env.SERVER || "http://127.0.0.1:5000"
const fileUpload = require('express-fileupload');
const cors = require('cors');
const bodyParser = require('body-parser');
const morgan = require('morgan');
const _ = require('lodash');
const { template } = require('lodash');
const { ClientRequest } = require('http');
const metricsInterval = Prometheus.collectDefaultMetrics()
const fetch = require('node-fetch');

const dbReportRequests = new Prometheus.Counter({
  name: 'dbReportRequests',
  help: 'Total number of dbReportRequests'
})

const dbReportErrors = new Prometheus.Counter({
  name: 'dbReportErrors',
  help: 'Total number of dbReportErrors'
})

app.use(fileUpload({
    createParentPath: true
}));

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(morgan('dev'));

app.get('/', (req, res) => {
  res.send('Index');
});


var api_data;
function setData(data){
  api_data = data;
}

app.get('/metrics', (req, res) => {
  res.setHeader('Content-Type', Prometheus.register.contentType)
  Prometheus.register.metrics().then(data => res.send(data))
})

//req template file and name for file (client id possibly)
app.post('/report', (req, res) => {
  const before = Date.now();
  try {
    let rawdata = req.files.data
    
    json_data = JSON.parse(rawdata.data)
    var options = {
      convertTo: 'pdf'
    };
    carbone.set({ converterFactoryTimeout: 0})
    carbone.render('./template-uploads/' + req.body.template, json_data, options, function(err, result){
      if (err) {
        return console.log(err);
      }
      // write the result
      fs.writeFileSync('./report-downloads/result.pdf', result);
      // send to client
      res.download('./report-downloads/result.pdf', function(err) {
        if(err) {
          console.log(err)
        }
        fs.unlink('./report-downloads/result.pdf', function(){
        })
        const after = Date.now();
        console.log('report gen executed in', (after - before) / 1000);

      })
    });
} catch (err) {
    res.status(500).send(err);
}
});
  

app.get('/db-report', async (req, res) => {
  try {
    dbReportRequests.inc()
    await fetch(SERVER + "/report_data?check_id=" + req.query.check_id, {
      method:'get'
      })
      .then((response) => response.json() )
      .then((data) => {
        setData(data)
      });

    var options = {
      convertTo : "pdf", //can be docx, txt, ...
      lang: "en-us",
      currencySource : "USD",
      currencyTarget : "USD"
    };

    carbone.set({ converterFactoryTimeout: 0 })
    carbone.render('./template-uploads/' + 'statment.odt', api_data, options, function(err, result){
      if (err) {
        return console.log(err);
      }
      // write the result
      fs.writeFileSync('/tmp/result.pdf', result);
      // send to client
      res.download('/tmp/result.pdf', function(err) {
        if(err) {
          console.log(err)
        }
        fs.unlink('/tmp/result.pdf', function(){
        })
      })
    });
} catch (err) {
  console.log(err)
  dbReportErrors.inc()
  res.status(500).send(err);
}
});


app.get('/db2-report', async (req, res) => {
  try {
    dbReportRequests.inc()
    await fetch(SERVER + "/pay_report", {
      method:'get'
      })
      .then((response) => response.json() )
      .then((data) => {
        setData(data)
      });

    var options = {
      convertTo : "pdf", //can be docx, txt, ...
      lang: "en-us"
    };

    carbone.set({ converterFactoryTimeout: 0 })
    carbone.render('./template-uploads/' + 'Demo2.odt', api_data, options, function(err, result){
      if (err) {
        return console.log(err);
      }
      // write the result
      fs.writeFileSync('/tmp/result.pdf', result);
      // send to client
      res.download('/tmp/result.pdf', function(err) {
        if(err) {
          console.log(err)
        }
        fs.unlink('/tmp/result.pdf', function(){
        })
      })
    });
} catch (err) {
  console.log(err)
  dbReportErrors.inc()
  res.status(500).send(err);
}
});


var files_arr;
app.get('/template', async (req, res) => {
  files_arr = []
  try {
    files_arr = (fs.readdirSync('./template-uploads/'))
    res.json({
        status: true,
        message: 'File is uploaded',
        files: files_arr
    });
} catch (err) {
    res.status(500).send(err);
}
});

//req template file and name for file (client id possibly)
app.post('/template', (req, res) => {
  const before = Date.now();
  try {
    console.log(req.body.files)
    console.log(req.files)
    if(!req.files) {
        console.log("no files")
        res.send({
            status: false,
            message: 'No file uploaded'
        });
    } else {
        //Use the name of the input field (i.e. "avatar") to retrieve the uploaded file
        let templateu = req.files.template;
        //Use the mv() method to place the file in upload directory (i.e. "uploads")
        templateu.mv('./template-uploads/' + templateu.name);
        //send response
        console.log("file uploaded")
        res.send({
            status: true,
            message: 'File is uploaded',
        });
    }
    const after = Date.now();
    console.log('template post executed in ', (after - before) / 1000);
} catch (err) {
    console.log("err")
    res.status(500).send(err);
}
});

//req template file and name for file (client id possibly)
app.delete('/template', (req, res) => {
  try {
        fs.unlink('./template-uploads/' + req.body.template, function(){
        })
        //send response
        res.send({
            status: true,
            message: 'template deleted',
        });
} catch (err) {
    res.status(500).send(err);
}
});

//req template file and name for file (client id possibly)
app.put('/template', (req, res) => {
  try {
        let template_ = req.files.template;
        fs.unlink('./template-uploads/' + template_.name, function(){
        })
        template_.mv('./template-uploads/' + template_.name);
        //send response
        res.send({
            status: true,
            message: 'template updated',
        });
} catch (err) {
    res.status(500).send(err);
}
});


if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
  });
}