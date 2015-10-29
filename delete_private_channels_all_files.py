# coding: utf-8
import yaml
import utils


def main():
    end_point = 'https://slack.com/api/'
    conf = yaml.load(open('conf.yaml').read())
    token = '?token=' + conf['token']
    your_name = conf['your_name']
    target_group_name = conf['group_name']

    # fetch users.list
    users_list = utils.fetch(end_point + 'users.list' + token)
    your_id = [member['id'] for member in users_list['members'] if member.get('name') == your_name][0]
    print('your_id:' + your_id)

    # fetch groups.list
    groups_list = utils.fetch(end_point + 'groups.list' + token)
    target_group_id = [group['id'] for group in groups_list['groups'] if group.get('name') == target_group_name][0]
    print('group_id: ' + target_group_id)

    # fetch files.list
    your_files_list = utils.fetch_all_files(end_point + 'files.list' + token + '&user=' + your_id)
    target_groups_your_files_list = [f for f in your_files_list if target_group_id in f.get('groups')]

    # show all your files, urls
    for f in target_groups_your_files_list:
        print(f['id'], f['url_private'])

    # files.delete
    print(' {0} 件削除します'.format(len(target_groups_your_files_list)))
    for f in target_groups_your_files_list:
        delete_status = utils.fetch(end_point + 'files.delete' + token + '&file=' + f['id'])
        print(delete_status)

    print('complete!!')


if __name__ == "__main__":
    main()