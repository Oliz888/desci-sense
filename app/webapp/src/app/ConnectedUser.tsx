import { Box, DropButton, Text } from 'grommet';
import { UserExpert } from 'grommet-icons';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { AppButton } from '../ui-components';
import { useThemeContext } from '../ui-components/ThemedApp';
import { cap } from '../utils/general';
import { useAccountContext } from './AccountContext';
import { OrcidAnchor } from './OrcidAnchor';
import { TwitterProfileAnchor } from './TwitterAnchor';

export const ConnectedUser = (props: {}) => {
  const { t } = useTranslation();
  const { isConnected, connect, disconnect, connectedUser } =
    useAccountContext();

  const { constants } = useThemeContext();

  const [showDrop, setShowDrop] = useState<boolean>(false);

  const parts = connectedUser?.orcid?.name.split(' ');
  const name = (() => {
    if (!parts) return '';
    if (parts.length > 2) return `${parts[0]} ${parts[2]}`;
    return `${parts[0]} ${parts[1]}`;
  })();

  const content = (() => {
    if (!isConnected) {
      return (
        <AppButton
          style={{ fontSize: '16px', padding: '6px 8px' }}
          label={t('connect')}
          onClick={() => connect()}></AppButton>
      );
    }

    return (
      <DropButton
        pad="small"
        label={
          <Box direction="row" align="center">
            <UserExpert
              color={constants.colors.primary}
              style={{ margin: '2px 0px 0px 5px' }}></UserExpert>
            <Text margin={{ left: 'small' }} style={{ flexShrink: 0 }}>
              {name}
            </Text>
          </Box>
        }
        open={showDrop}
        onClose={() => setShowDrop(false)}
        onOpen={() => setShowDrop(true)}
        dropContent={
          <Box pad="20px" gap="small" style={{ width: '220px' }}>
            <Box margin={{ bottom: 'small' }}>
              <Text>{cap(t('orcid'))}</Text>
              <OrcidAnchor orcid={connectedUser?.orcid?.orcid}></OrcidAnchor>
            </Box>

            <Box margin={{ bottom: 'small' }}>
              <Text>{cap(t('twitter'))}</Text>
              <TwitterProfileAnchor
                screen_name={
                  connectedUser?.twitter?.screen_name
                }></TwitterProfileAnchor>
            </Box>

            <AppButton
              plain
              onClick={() => disconnect()}
              style={{ textTransform: 'none', paddingTop: '6px' }}>
              <Text style={{ fontWeight: 'bold' }}>{cap(t('logout'))}</Text>
            </AppButton>
          </Box>
        }
        dropProps={{
          style: { marginTop: '3px' },
          align: { top: 'bottom' },
        }}></DropButton>
    );
  })();

  return (
    <Box style={{ height: '60px' }} align="center" justify="center">
      {content}
    </Box>
  );
};
