"""Utils regarding git using pygit2."""

DEFAULT_BRANCH_NAMES = ('master', 'main')


def get_local_branch_name(remote_branch):
    """Get the local branch name associated with a remote branch.

    :param remote_branch: Remote branch you want the local name of.
    :type remote_branch: pygit2.Branch

    :raises ValueError: Provided branch is not a remote one.

    :return: Local branch name.
    :rtype: str.
    """
    return remote_branch.branch_name[len(f'{remote_branch.remote_name}/'):]


def get_remote_name(branch):
    """Get the remote name of a branch.

    :param branch: Branch you want the remote name of.
    :type branch: pygit2.Branch

    :return: The name of the remote the branch is associated to, returns None
             if the branch is a local one.
    :rtype: str, None
    """

    # As pygit2 is far from perfect the branch.type attribute always says that
    # it is a local branch. The only way I found is to attempt to access the
    # remote_name which, in case the branch is local, will raise a ValueError.
    try:
        # Try to access the remote name.
        return branch.remote_name
    except ValueError:
        # Accessing remote_name failed, branch is local one.
        return None


def is_branch_remote(branch):
    """Determine if the branch is a remote one.

    :param branch: Branch you want to know if it is a remote one.
    :type branch: pygit2.Branch

    :return: True if the branch is a remote one, False otherwise.
    :rtype: bool
    """
    return bool(get_remote_name(branch))


def is_rebased_on(repository, reference, target):
    """Find out if a specific reference is rebased on top of a specific target
    reference.

    :param repository: Repository the reference are in.
    :type repository: pygit2.Repository
    :param reference: Git reference you want to know if it is rebased on
                      target.
    :type reference: str
    :param target: Git reference you want to know if reference in rebased on.
    :type target: str

    :return: True if reference is rebased on target, False otherwise.
    :rtype: bool
    """
    return repository.merge_base(target, reference) == target
