var express = require('express'); 
var app = express();
var mongoose = require('mongoose');
var path = require('path');
var formidable = require('formidable');
var gridform = require('gridform');
const multer = require('multer');
const GridFsStorage = require('multer-gridfs-storage');
const Grid = require('gridfs-stream');
const methodOverride = require('method-override');
const bodyParser = require('body-parser');

//gridform.db = db;
//gridform.mongoose = mongoose;

var url = "mongodb://localhost:27017/test";


app.use(bodyParser.json());
app.use(methodOverride('_method'));
app.set('view engine', 'ejs')



let gfs;

const conn = mongoose.createConnection(url)

conn.once('open', () => {
    gfs = Grid(conn.db, mongoose.mongo);
    gfs.collection('uploads');
});


const storage = new GridFsStorage({
    url: url,
    file: (req, file) => {
        return new Promise((resolve, reject) => {
            const filename = file.originalname;
            const fileInfo = {
                filename: filename,
                bucketName: 'uploads'
            };
            resolve(fileInfo);
        });
    }
});

const upload = multer({ storage });

app.get('/', (req, res) => {
    gfs.files.find().toArray((err, files) => {
        if (!files || files.length === 0) {
            res.render('index', {files: false});
        } else {
            files.map(file => {
                if (
                    file.contentType === 'image/jpeg' ||
                    file.contentType == 'image/png'
                ) {
                    file.isImage = true;
                } else {
                    file.isImage = false;
                }
            });
            res.render('index', { files: files });
        }
    })
})

app.get('/image/:filename', (req, res) => {
    gfs.files.findOne({ filename: req.params.filename }, (err, file) => {
      // Check if the input is a valid image or not
      if (!file || file.length === 0) {
        return res.status(404).json({
          err: 'No file exists'
        });
      }
  
      // If the file exists then check whether it is an image
      if (file.contentType === 'image/jpeg' || file.contentType === 'image/png') {
        // Read output to browser
        const readstream = gfs.createReadStream(file.filename);
        readstream.pipe(res);
      } else {
        res.status(404).json({
          err: 'Not an image'
        });
      }
    });
  });
  
  // delete function to remove the file from the database
  app.delete('/files/:id', (req, res) => {
    gfs.remove({ _id: req.params.id, root: 'uploads' }, (err, gridStore) => {
      if (err) {
        return res.status(404).json({ err: err });
      }
  
      res.redirect('/');
    });
  });

app.listen(3000, function() {
    console.log("Server is running on port 3000");
});

app.get('/files', (req, res) => {
    gfs.files.find().toArray((err, files) => {
        if (!files || files.length === 0) {
            return res.status(404).json({
                err: 'No files exist'
            });
        }
    })
})

app.post('/upload', upload.single('file'), (req, res) => {
    res.redirect('/');
});

/*

app.get('/', function(request, response) {
    response.sendFile('core.html', {root: path.join(__dirname)});
})

app.post('/submit-form', (req, res) => {
    new formidable.IncomingForm().parse(req, (err, fields, files) => {
        if (err) {
            console.error('Error', err);
            throw err;
        }
        console.log("Fields", fields);
        console.log('Files', files);
        for (const file of Object.entries(files)) {
            console.log(file);
        }
    })
});

*/

/*
mongoose.connect(url, { useNewUrlParser: true, useCreateIndex: true });
const connection = mongoose.connection;
connection.once('open', () => {
    console.log('connected to database');
})
*/