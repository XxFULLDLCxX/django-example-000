window.onpopstate = function (event) {
    console.log("Onpopstate");
    showSection(event.state.section);
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function showSection(id) {
    fetch(`/api/section/${id}`, {
            method: "POST",
            mode: "same-origin",
            headers: {
                "X-CSRFToken": csrftoken
            }
        })
        .then(res => res.text())
        .then(res => content.innerHTML = res);
    setTimeout(function () {
        load.style = 'animation-duration: 30s;'
    }, 500);

}


document.addEventListener('DOMContentLoaded', function () {
    load = document.querySelector('.load')
    content = document.querySelector('#content');
    document.querySelectorAll('.section').forEach(button => {
        button.onclick = function () {
            const id = this.dataset.id;
            //document.querySelector('title').innerHTML = this.textContent;
            load.style = 'animation-duration: 0.1s;'
            history.pushState({ id: id }, "", `/?section=${id}`);
            showSection(id);

        };
    });


});