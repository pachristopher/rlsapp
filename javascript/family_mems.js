let addBtn = document.getElementById('add_family_member');
let familyMembersDiv = document.getElementById('family_members');
let familyMemberCount = 1;

addBtn.addEventListener('click', function() {
  let firstFamilyMember = document.querySelector('.family_member');
  let newFamilyMember = firstFamilyMember.cloneNode(true);

  let inputs = newFamilyMember.querySelectorAll('input, select');
  inputs.forEach(function(input) {
    let name = input.getAttribute('name').replace('0', familyMemberCount);
    input.setAttribute('name', name);
    let id = input.getAttribute('id').replace('0', familyMemberCount);
    input.setAttribute('id', id);
    input.value = '';
  });

  familyMembersDiv.appendChild(newFamilyMember);
  familyMemberCount++;
});

