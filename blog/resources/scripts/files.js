function deleteFile(filename) {
    if (confirm(`Вы уверены, что хотите удалить файл ${filename}?`)) {
        fetch(`/delete_file/${filename}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Обновить страницу или выполнить другие действия по желанию
                location.reload();
            } else {
                alert('Не удалось удалить файл.');
            }
        })
        .catch(error => console.error('Ошибка:', error));
    }
}