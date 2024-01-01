        document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function () {
        const itemID = this.id.replace('btn', '');
        fetch('/api/get_item/${itemID}/')
            .then(response => response.json())
            .then(data => {
                const priceElement = document.createElement('p');
                priceElement.textContent = 'Mahsulot nomi: ${data.nomi}, Narxi: ${data.narhi}';
                const itemDiv = this.closest('.item');
                itemDiv.appendChild(priceElement);
            })
            .catch(error => {
                console.error('Xatolik:', error);
            });
    });
});