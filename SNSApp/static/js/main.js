// 投稿カードクリックで詳細へ
document.querySelectorAll('.post-card').forEach(card => {
    card.addEventListener('click', function (e) {

        // ブックマークを押した場合は遷移しない
        if (e.target.closest('.bookmark-btn')) {
            return;
        }

        const url = this.dataset.url;
        window.location.href = url;
    });
});


// ブックマーク処理
document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {

        e.stopPropagation(); // 親に伝えない

        const postId = this.dataset.postId;

        fetch(`/bookmark/${postId}`, {
            method: "POST"
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "bookmarked") {
                this.textContent = "★";
            } else {
                this.textContent = "☆";
            }
        });
    });
});


// document.querySelectorAll('.bookmark').forEach(btn => {
//     btn.addEventListener('click', (e) => {
//         e.stopPropagation(); // ← これ！
//         // お気に入り処理
//     });
// });