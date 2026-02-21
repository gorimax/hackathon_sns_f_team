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

// ==========================
// 要素取得
// ==========================
const modalToggle = document.getElementById("new-post");
const form = document.querySelector(".post-form");
const checkboxes = document.querySelectorAll('input[name="tag_ids[]"]');



function toggleCheckboxes() {
    const box = document.getElementById("checkboxes");
    box.style.display = box.style.display === "none" ? "block" : "none";
}

/* ここが重要 */
document.addEventListener("click", function(event) {
    const multiselect = document.querySelector(".multiselect");
    const checkboxes = document.getElementById("checkboxes");

    // クリックされた場所がマルチセレクトの外なら閉じる
    if (!multiselect.contains(event.target)) {
        checkboxes.style.display = "none";
    }
});

function updateSelectedTags() {
    const checked = document.querySelectorAll('input[name="tag_ids[]"]:checked');
    const selectedDiv = document.getElementById("selected-tags");

    if (checked.length > 3) {
        alert("タグは最大3つまでです");
        checked[checked.length - 1].checked = false;
        return;
    }

    let names = [];
    checked.forEach(cb => {
        names.push(cb.parentElement.textContent.trim());
    });

    selectedDiv.textContent = names.length > 0
        ? names.join(", ")
        : "タグを選択してください（最大3つ）";
}


let expanded = false;
function showCheckboxes() {
    let checkboxes = document.getElementById("checkboxes");
    if (!expanded) {
        checkboxes.style.display = "block";
        expanded = true;
    } else {
        checkboxes.style.display = "none";
        expanded = false;
    }
}


// ==========================
// 最大3つ制限 + 表示更新
// ==========================
checkboxes.forEach(cb => {
    cb.addEventListener("change", function () {

        const checked = document.querySelectorAll(
            'input[name="tag_ids[]"]:checked'
        );

        if (checked.length > 3) {
            alert("タグは最大3つまで選択できます");
            this.checked = false;
            return;
        }

        updateSelectedTags();
    });
});


// ==========================
// モーダル初期化
// ==========================
function resetModal() {

    form.reset();

    checkboxes.forEach(cb => cb.checked = false);

    selectedTagsDiv.innerHTML =
        '<span class="no-tag-message">タグ表示欄です</span>';
}


// ==========================
// モーダル閉じたらリセット
// ==========================
modalToggle.addEventListener("change", function () {
    if (!this.checked) {
        resetModal();
    }
});