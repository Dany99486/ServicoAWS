import axios from 'axios'

function DataFetchPut(url,data) {
        url='http://estrabalho.us-east-1.elasticbeanstalk.com/' + url;

        //access token saved in local storage, if not exists return null
        let token=localStorage.getItem("token")
        
        //with authentication and send json
        if (token!=null){
            return new Promise((resolve, reject) => {
                axios.put(url,data,{
                    headers:{
                        Authorization:token
                    }
                })
                .then(response=>{resolve({success:"yes",data:response['data']})})
                .catch(error=>{reject({success:"no",error:error})});
        })
        }
        else{
            //without authentication and send json
            return new Promise((resolve,reject)=>{
                axios.put(url,data)
                .then(response=>{resolve({success:"yes",data:response['data']})})
                .catch(error=>{reject({success:"no",error:error})});
            })      
        }
}

export default DataFetchPut;