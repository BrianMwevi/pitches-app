$(document).ready(function () {
  $('.vote').click(toggleVote);
  $('.comment-form').submit(createComment);
})

const toggleVote = (e) => {
  const user_id = $('.user_id').attr('id');
  if (user_id) {
    const [vote, pitch_id] = e.currentTarget.id.split(' ')
    return postLike(pitch_id.slice(-1), vote)    
  }
  return false;
}

const postLike = (pitch_id, vote)  => {
  const likes = $(`.count-likes${pitch_id}`);
  const dislikes = $(`.count-dislikes${pitch_id}`);
  const url = `/pitch/${vote}/${pitch_id}`;
  $.post(url, function (data) {
  likes.text(data[0])
  dislikes.text(data[1])
  })

}

const createComment = e => {
  e.preventDefault()
  const pitch_id = e.currentTarget.id.slice(-1,12)
  const url = `/comment/${pitch_id}/add`
  const form = $('#commentForm' + pitch_id)
  const data = form.serialize()
  $.post(url, data, function (newComment) {
    
  const comment = `<p class="pl-3"><span class="badge badge-secondary custom-color">By @${newComment.user}</span> <small>${newComment.body}</small></p>`
    $(`.comment-section${pitch_id}`).prepend(comment)
    return form.trigger('reset')
  } )

}

