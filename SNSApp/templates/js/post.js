document.querySelectorAll('.post-card').forEach(card => {
    card.addEventListener('click', () => {
        window.location.href = card.dataset.url;
    });
});

document.querySelectorAll('.bookmark').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.stopPropagation(); // ← これ！
        // お気に入り処理
    });
});