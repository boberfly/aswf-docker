# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
import logging
import typing

from github import Github

from aswfdocker import settings, constants, aswfinfo, groupinfo

logger = logging.getLogger(__name__)


class GitHub:
    def __init__(self):
        s = settings.Settings()
        if s.github_access_token:
            self.github = Github(s.github_access_token)
        else:
            self.github = Github()
        self.repo = self.github.get_repo(constants.GITHUB_REPO)

    def create_release(self, sha, tag, release_message, prerelease):
        logger.debug("GitHub.create_release(tag=%s)", tag)
        self.repo.create_git_tag_and_release(
            tag.replace(":", "/"),
            tag_message=tag,
            release_name=tag,
            release_message=release_message,
            object=sha,
            type="commit",
            draft=False,
            prerelease=prerelease,
        )


class Releaser:
    """Releaser creates GitHub releases for each docker image.
    """

    def __init__(
        self, build_info: aswfinfo.ASWFInfo, group_info: groupinfo.GroupInfo, sha: str
    ):
        self.build_info = build_info
        self.group_info = group_info
        self.sha = sha
        self.gh = GitHub()
        self.release_list: typing.List[typing.Tuple[str]] = []

    def gather(self):
        for image, version in self.group_info.iter_images_versions():
            tag = f"{self.build_info.docker_org}/{image}:{version}"
            self.release_list.append((image, version, tag))

    def release(self, dry_run=True):
        logger.debug("Releaser.release(dry_run=%s)", dry_run)
        prerelease = self.build_info.docker_org == constants.TESTING_DOCKER_ORG
        for image, version, tag in self.release_list:
            message = f"Inspect released docker image here: https://hub.docker.com/r/{self.build_info.docker_org}/{image}/tags?name={version}"
            if dry_run:
                logger.info(
                    "Would create this GitHub release on current commit: %s", tag
                )
            else:
                self.gh.create_release(
                    self.sha, tag, release_message=message, prerelease=prerelease
                )