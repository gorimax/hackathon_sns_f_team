// 投稿カードクリックで詳細へ
document.querySelectorAll('.post-card').forEach(card => {
    card.addEventListener('click', function (e) {

        // ブックマークを押した場合は遷移しない
        if (e.target.closest('.bookmark-btn') || 
            e.target.closest('.tag')) {
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


// 投稿画面のタグ選択
const select = document.getElementById("tag-select");
const selectedTagsDiv = document.getElementById("selected-tags");

select.addEventListener("change", function() {

    selectedTagsDiv.innerHTML = ""; // 既存のタグをクリア

    const selectedOptions = Array.from(this.selectedOptions);

    // 何も選ばれていない場合
    if (selectedOptions.length === 0){
        const message = document.createElement("span");
        message.classList.add("no-tag-message");
        message.textContent = "タグを選択してください";
        selectedTagsDiv.appendChild(message);
        return;
    }

    // 選択されている場合
    selectedOptions.forEach(option => {
        const tag = document.createElement("span");
        tag.classList.add("tag-item");
        tag.textContent = option.value;
        selectedTagsDiv.appendChild(tag);
    });

});
// document.querySelectorAll('.bookmark').forEach(btn => {
//     btn.addEventListener('click', (e) => {
//         e.stopPropagation(); // ← これ！
//         // お気に入り処理
//     });
// });