from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(value, decimal):
    try:
        format_str = '{0:.'+ str(decimal) + '%}'
        return format_str.format(value)
    except:
        return value
# url:'http://127.0.0.1:8000/visual/show_data',




# <script type="text/javascript">
#                 $("#AJAX_get").click(function (event) {
#                     event.preventDefault(); // 防止表单默认的提交
#                     // 获取单选下拉框的值
#                     alert('所选维度为: ' + $("#Feature1").val() + ' 和 ' + $("#Feature2").val() +
#                     '\n' + '所选辅助维度为: ' + $("#Feature_opt").val());
#                     var form_data = {
#                         "Feature1": $("#Feature1").val(),
#                         "Feature2": $("#Feature2").val(),
#                         "Feature_opt": $("#Feature_opt").val(),
#                     };
#                 })
#                 $("#show_data").click(function (event) {
#                     event.preventDefault(); // 防止表单默认的提交
#                     // 获取单选下拉框的值
#                     alert('hhh');
#
#                 })
#             </script>