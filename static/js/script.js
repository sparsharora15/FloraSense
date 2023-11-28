function preview(id) {

    document.querySelector('#' + id).addEventListener('change', function(e) {

        if (e.target.files.length == 0) {
            return;
        }

        let file = e.target.files[0];
        let url = URL.createObjectURL(file);
        preview = document.querySelector('#' + id + '-bg');
        preview.style.backgroundImage = "url('" + url + "')";


    })
}

preview('plant')
preview('disease')