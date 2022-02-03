
function like_post(event) {

    event.preventDefault();

    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let formData = new FormData();
    formData.append('mylikeid', document.querySelector("#mylikeid").className);

    const request = new Request('like/', {
        method: 'POST',
        credentials: 'same-origin',
        body: formData,
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
        }  // We add the token to the header
    });

    fetch(request)
        .then(response => {
            return response.json() //Convert response to JSON
        })
        .then(data => {
            console.log(data['post_like_toggle'])
            //Perform actions with the response data from the view
            const likeCount = document.getElementById("like_count");

            if (data['post_like_toggle']==="like"){
                document.getElementById("mylikeid").className="fas fa-heart";
                likeCount.innerHTML = (parseInt(likeCount.textContent)+1).toString();
            }else{
                document.getElementById("mylikeid").className="far fa-heart";
                likeCount.innerHTML = (parseInt(likeCount.textContent)-1).toString();
            }
        })
}


function comment_post(event){

    event.preventDefault();

    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let formData = new FormData();

    formData.append('txtAreaComment', document.getElementById("txtAreaComment").value);
    formData.append('author_id', com_author_id);
    formData.append('author_name', com_author_name);

    const request = new Request('comment/', {
        method: 'POST',
        credentials: 'same-origin',
        body: formData,
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
        }
    });

    fetch(request)
        .then(response => {
            return response.json() //Convert response to JSON
        })
        .then(data => {

            let new_node_com_author = document.createElement("h6");
            let new_node_com_text = document.createElement("p");

            new_node_com_author.textContent = data['com_author']+" - "+data['com_date'];
            new_node_com_text.textContent = data['com_text'];

            let parentElement = document.getElementById("box_commentaire")
            let theFirstChild = parentElement.firstChild

            parentElement.insertBefore(new_node_com_author, theFirstChild)
            parentElement.insertBefore(new_node_com_text, theFirstChild)

        })
}