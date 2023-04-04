let categorySelect = document.getElementById('categorySelect')

categorySelect.addEventListener('change', async function(){
    let categorySelectValue = categorySelect.value;
    try {
        const response = await fetch('/courses?' + new URLSearchParams({
            category: categorySelectValue
        }))
        const coursesDiv = document.getElementById('courses');
        coursesDiv.innerHTML = await response.text();
        console.log(response)
    }catch (e){
        console.log(e)
    }
})