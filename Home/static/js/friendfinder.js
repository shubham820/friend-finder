console.log("shubham");
function postLikeorNot(e)
{
   id = e.toString()  
   
   const xhr = new XMLHttpRequest()
   xhr.open('GET' , `/profile/post_like/${id}` ,true)
   xhr.send()
   xhr.onreadystatechange = function ()
   {
      if (xhr.readyState == 4 && xhr.status == 200)
      {
         const like_wala_element = document.getElementById(`likes${id}`)
         like_wala_element.innerText = xhr.responseText       
      }
   }
}
function PostComment(cmt)
{
    id = e.toString()

   const xhr = new XMLHttpRequest()
   xhr.open('POST' , `/profile/Post_comment/` ,true)
   xhr.send()
   xhr.onreadystatechange = function ()
   {
      if (xhr.readyState == 4 && xhr.status == 200)
      {
         const like_wala_element = document.getElementById(`likes${id}`)
         like_wala_element.innerText = xhr.responseText
      }
   }



}


// console.log(sessionStorage.getItem("user"))
         // console.log(typeof this.response)
         // const event = document.getElementById(id)
         // event.
         // location.reload(); 
         // preventDefault()
         // let asdc = `127.0.0.1:8000/profile/post_like/${id}`
         // console.log(asdc)
         // const dom = new DOMParser()
         // const updatedom = dom.parseFromString(updatedText,"text/html") 
         // console.log(updatedText,7777777777777)
         // const avc = document.getElementById(id)
         // console.log(typeof this.response)
         // console.log(avc.parentElement.innerHTML)
         // let resptext = xhr.getResponseHeader
         // const like_wala_element = document.getElementById(`likes${id}`)
         // like_wala_element.innerText = xhr.responseText 
         // document = updatedom
         // console.log(document)
         // const let = new XMLHttpRequest()
         // let.open('GET' , `/profile/` ,true)
         // let.send()   