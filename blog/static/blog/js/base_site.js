function search_validator(form) {
	var value = form.keyword.value;
	if (valuue === null || value === ''){
		alert('搜索参数不能为空')
		return false ;
	}
	return true;
}