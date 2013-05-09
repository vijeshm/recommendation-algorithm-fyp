#ifndef DISPLAYY3_H
#define DISPLAYY3_H

#include <QWidget>

namespace Ui {
class displayy3;
}

class displayy3 : public QWidget
{
    Q_OBJECT
    
public:
    explicit displayy3(QWidget *parent = 0);
    ~displayy3();
    
private:
    Ui::displayy3 *ui;
};

#endif // DISPLAYY3_H
