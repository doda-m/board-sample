function check(){
  var a=document.messege.content.value;
  if(a==""){
    return false;
  }else if(!a.match(/\S/g)){
    return false;
  }
//   else if(!a.match(/\n/g)){
//     return false;
//   }
}