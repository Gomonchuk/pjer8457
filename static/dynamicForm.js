	let nameCount = 0;

	function isValidName(name) {
   	    const nameRegex = /^[A-Za-zА-Яа-яЁё\s'-]+$/;//regex нашел в сети:)
	    return nameRegex.test(name);
	}
	function inputError(WhichInput,textOfError){
		

	}
        $(document).ready(function() {
            //Добавление нового инпута
            $('.dynamicForm_addInput').click(function() {
		nameCount++;
                $('.dynamicForm_inputs').append(`
                        <input class="dynamicForm_input" type="text" name="name${nameCount}" placeholder="Введите имя №${++nameCount}" required>
                `);
            });

            //Обработка отправки формы или форм
            $('.dynamicForm').submit(function(event) {
                event.preventDefault(); 
                const formData = $(this).serializeArray();
		let values_formData = [];
		formData.forEach(function(item){
			console.log(item);
			if(isValidName(item.value)){
				values_formData.push(item.value);
			}else{
				//я бы здесь подсвечивал красным input где пользователь вместо имени ввел какуюту дребедень с помощью стилей   
				alert(item.value + " не является именем и не будет сохранён в базе данных");
			} 
		});
                const jsonData = JSON.stringify(values_formData);
                $.ajax({
                    type: 'POST',
                    url: '/handler',
                    contentType: 'application/json',
                    data: JSON.stringify({ inputs: jsonData }),
                    success: function(response) {
                        alert('Данные успешно сохранены!');
                    },
                    error: function(error) {
                        alert('Ошибка при сохранении данных.');
                    }
                });
            });
        });

