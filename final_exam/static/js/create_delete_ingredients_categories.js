document.addEventListener("DOMContentLoaded", function() {
        function delete_parent(event){
            event.preventDefault();
            event.currentTarget.parentNode.remove();
        }

        let container = document.getElementById('ingredient-forms');
        let button_add = container.querySelector('#add-ingredient');
        let my_form = container.querySelector('.ingredient-group').cloneNode(true);
        let delete_button = container.querySelector('.remove-ingredient');
        delete_button.addEventListener('click', delete_parent);

        button_add.addEventListener('click', (event) => {
            event.preventDefault();
            let clone_form = my_form.cloneNode(true);
            container.append(clone_form);
            let new_delete_button = clone_form.getElementsByClassName('remove-ingredient')[0];
            new_delete_button.addEventListener('click', delete_parent);
        });

        let category_container = document.getElementById('category-forms');
        let category_button_add = category_container.querySelector('#add-category');
        let category_form = category_container.querySelector('.category-group').cloneNode(true);
        let category_delete_button = category_container.querySelector('.remove-category');
        category_delete_button.addEventListener('click', delete_parent);

        category_button_add.addEventListener('click', (event) => {
            event.preventDefault();
            let clone_form = category_form.cloneNode(true);
            category_container.append(clone_form);
            let new_delete_button = clone_form.getElementsByClassName('remove-category')[0];
            new_delete_button.addEventListener('click', delete_parent);
        });
    });