import './App.css';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import fetch from 'node-fetch'

import React, { useEffect, useState} from "react"

const SERVER = process.env.REACT_APP_SERVER || "http://127.0.0.1:5000"
const API = process.env.REACT_APP_API || "http://127.0.0.1:3000"

var offset = 0;
var buffer = '';
var records = 0;
function App() {

  function nextPage() {
    fetchData()
    offset += 10;
  }

  function prevPage() {
    fetchData()
    if (offset !== 0){
      offset -= 10;
    }
  }

  function refresh() {
    fetchData()
  }

  function getOffset(){
    return offset
  }

  function getSearch(){
    return buffer;
  }

  const submit = (e) =>{
    fetchData()
    e.preventDefault();
    buffer = search
  }

  function clearSearch(){
    fetchData()
    setSearch("");
    buffer = ''
  }

  const [users, setUsers] = useState([])
  const [search, setSearch] = useState("")
  const [records, setRecords] = useState("")

  const fetchData = () => {

    fetch(SERVER + "/table_data?offset=" + getOffset() + "&search=" + getSearch(), {method:'get', headers: {'Content-Type': 'application/json'}})
      .then((response) => {
        return response.json()
      })
      .then((data) => {
        setUsers(data)
      });

    fetch(SERVER + "/users", {method:'get', headers: {'Content-Type': 'application/json'}})
      .then((response) => {
        return response.json()
      })
      .then((data) => {
        setRecords(data)
      });

  }

  useEffect(() => {
    fetchData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  function getReport(check_id) {
    fetch(API + "/db-report?check_id=" + check_id, {
      method:'get'
      })
      .then((response) => response.blob())
      .then((blob) => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        //a.download = "statement.pdf";
        const pdfWindow = window.open();
        pdfWindow.location.href = a.href;  
        
        a.remove();  //afterwards we remove the element again
      });
  }

  return (
    <div className="App">
      <header className="App-header">
        <div class="head">
          <h1>
            Demo 1 
          </h1>
        </div>
        <hr></hr>

        <div>
          <div class="form">
            <form onSubmit={submit}>
              <label>
                ID:
                <input type="text" onChange={(e) => setSearch(e.target.value)} />
              </label>
              <input type="submit" value="Search" />

            </form>

          </div>
          <Button onClick={clearSearch}>Clear Search</Button>
          <Button onClick={refresh}>Refresh</Button>
        </div>
       

        <div class="table-block">
          <div class='buttons'>
              <Button onClick={prevPage}>Prev Page</Button>
              <p>Total Records: {records['count_1']}</p> 
              <Button onClick={nextPage}>Next Page</Button>
          </div>

          <table class="styled-table">
              <tr class="styled-tr">
                  <th>Val 1</th>
                  <th>Val 2</th>
                  <th>Val 3</th>
                  <th>Val 4</th>
                  <th>Val 5</th>
                  <th>Val 6</th>
              </tr>

            {users.map(users => (
            <tr class="styled-tr">
              <td>{users.Val1}</td>
              <td>{users.Val2}</td>
              <td>{users.Val3}</td>
              <td>{users.Val4}</td>
              <td>{users.Val5}</td>
              <th><Button onClick={() => getReport(users.Val6)}>View Check</Button></th>
            </tr>

            ))}
          </table>
        </div>
      </header>
    </div>
  );
}

export default App;
